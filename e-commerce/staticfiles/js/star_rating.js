document.addEventListener('DOMContentLoaded', () => {
	// Obtén todos los elementos con la clase 'sp'
    const spanParaEstrellas = document.querySelectorAll('span.sp');

    // Recorre cada elemento y realiza una solicitud fetch para obtener la puntuación del producto
    spanParaEstrellas.forEach(async (element) => {
        // Obtén el ID del producto desde algún lugar (puedes agregar un atributo 'data-product-id' en el HTML)
        const productId = element.getAttribute('data-product-id');
        drawStars(productId, element);
        puntuar(element);
    });


	function puntuar(element) {
		element.querySelectorAll('.fa').forEach((star) => {
            star.addEventListener('click', (event) => {
                const puntuacion = parseInt(event.target.dataset.index) + 1;
                const prodId = element.getAttribute('data-product-id');
                
                fetch(`http://localhost:8000/api/products/${prodId}/${puntuacion}`, {method: 'PUT'})
                    .then(response => response.json())
                    .then(() => {
                        drawStars(prodId, element);                    
                    })
                    .catch(error => {
                        console.error('Error al realizar PUT:', error);
                    });
            });

            star.addEventListener('mouseover', (event) => {
                const index = parseInt(event.target.dataset.index);
                const stars = element.querySelectorAll('.fa');

                stars.forEach((star, i) => {
                    if (i <= index) {
                        star.classList.add('checked');
                    } else {
                        star.classList.remove('checked');
                    }
                });
            });

            star.addEventListener('mouseout', (event) => {
                const stars = element.querySelectorAll('.fa');

                stars.forEach((star) => {
                    star.classList.remove('checked');
                });
            });
        });
	}

	async function drawStars(productId, element) {
		try {
            // Realiza una solicitud fetch a tu API para obtener la puntuación del producto
            const response = await fetch(`http://localhost:8000/api/products/${productId}`);
            const data = await response.json();
    
            // Verifica si la solicitud fue exitosa y si hay una puntuación en la respuesta
            if (response.ok && data.length > 0) {
                const ratingValue = data[0].rating.rate;
                const ratingCount = data[0].rating.count;
                let num_star = 0;
                let max_star = 5;
    
                element.innerHTML = '';

                for (let i = 1; i <= ratingValue; i++) {
					element.innerHTML += `<span class="fa fa-star" data-index="${num_star}"></span>`;
					num_star++;
				}

				if (ratingValue % 1 >= 0.5) {
					element.innerHTML += `<span class="fa fa-star-half-o" data-index="${num_star}"></span>`;
					num_star++;
				}

				let last_stars = max_star - num_star;
				for (let i = 0; i < last_stars; i++) {
					element.innerHTML += `<span class="fa fa-star-o" data-index="${num_star}"></span>`;
					num_star++;
				}

                element.innerHTML += `<span class="rate">${Number((ratingValue).toFixed(1))}(${ratingCount})</span>`;

                // Event listener para cada estrella
                puntuar(element);

            } else {
                console.error(`Error al obtener la puntuación para el producto ${productId}`);
            }
        } catch (error) {
            console.error('Error en la solicitud fetch:', error);
        }
	}

	function handleStarClick(starIndex) {
		console.log('Número del elemento seleccionado:', starIndex);
	}
});