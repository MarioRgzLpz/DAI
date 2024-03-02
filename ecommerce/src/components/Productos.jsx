import React, { useState, useEffect, useCallback } from 'react';
import { Card, Button, Row, Col } from 'react-bootstrap';
import { Rating } from 'primereact/rating';
import 'primeicons/primeicons.css';

const ProductList = ({ searchTerm, selectedCategory }) => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);

  const fetchData = useCallback(async () => {
    try {
      const response = await fetch('http://localhost/api/products?desde=0&hasta=50');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    // Filtrar productos por título y categoría cuando searchTerm o selectedCategory cambian
    const filtered = products.filter(
      (product) =>
        product.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
        (selectedCategory ? product.category === selectedCategory : true)
    );
    setFilteredProducts(filtered);
  }, [searchTerm, selectedCategory, products]);


  const handleRatingChange = async (event) => {
    const productId = event.target.id; // Asegúrate de que el id esté disponible en tus datos
    const newRating = event.value;

    // Realiza la solicitud a la API para actualizar la puntuación
    try {
      const response = await fetch(`http://localhost/api/products/${productId}/${newRating}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating: newRating }),
      });

      if (response.ok) {
        // Actualiza localmente la puntuación y el conteo
        const updatedProducts = filteredProducts.map((product) => {
          if (product.id === productId) {
            return {
              ...product,
              rating: {
                count: product.rating.count + 1, // Incrementa el conteo
                rate: (product.rating.rate*product.rating.count + newRating)/(product.rating.count + 1)
              },
            };
          }
          return product;
        });

        setFilteredProducts(updatedProducts);
      } else {
        console.error('Error updating rating:', response.status);
      }
    } catch (error) {
      console.error('Error updating rating:', error);
    }
  };

  return (
    <div className="mx-auto" style={{ maxWidth: 'calc(75% - 200px)', marginTop: '100px' }}>
      <Row xs={1} md={4} className="g-2">
      {filteredProducts.map((product) => (
          <Col key={product.id}>
            <Card className="d-flex flex-column h-100">
              <Card.Body className="d-flex flex-column align-items-center">
                <Card.Img variant="top" src={product.image} alt={product.title} /> 
                <Card.Title>{product.title}</Card.Title>
                <Card.Text>{product.description}</Card.Text>
                <Rating
                  value={product.rating.rate}
                  onChange={handleRatingChange}
                  id={product.id.toString()}
                  cancel={false}
                />
                <Card.Text>({product.rating.count})</Card.Text>
              </Card.Body>
              <Card.Footer className="d-flex justify-content-between align-items-center">
                <Button variant="primary">Comprar</Button>
                <p className="m-0" style={{ color: 'red' }}>{product.price} €</p>
              </Card.Footer>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default ProductList;