import React, { useState, useEffect } from 'react';
import { Navbar, Container, Nav, Form, FormControl, Button ,NavDropdown} from 'react-bootstrap';

const NavbarMenu = ({ onSearch, onSelectCategory }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [categories, setCategories] = useState([]);

  const handleSearch = () => {
    // Llama a la función onSearch del componente padre con el término de búsqueda
    onSearch(searchTerm);
  };

  useEffect(() => {
    // Esta función se encarga de extraer las categorías únicas de la lista de productos
    const extractCategories = (products) => {
      const uniqueCategories = Array.from(new Set(products.map((product) => product.category)));
      setCategories(uniqueCategories);
    };

    // Realiza la solicitud para obtener los productos
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost/api/products?desde=0&hasta=50');
        const data = await response.json();
        extractCategories(data);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    // Llama a la función para obtener los productos
    fetchProducts();
  }, []);

    return (
        <Navbar bg="dark" variant="dark" fixed="top">
            <Container>
                <Navbar.Brand href="/">Mi Tienda</Navbar.Brand>
                <div style={{ margin: '0 150px' }}></div>
                <Navbar.Collapse >
                    <Nav>
                        <NavDropdown title="Categorías" id="basic-nav-dropdown">
                        {categories.map((category) => (
                            <NavDropdown.Item key={category} onClick={() => onSelectCategory(category)}>
                            {category}
                            </NavDropdown.Item>
                        ))}
                        </NavDropdown>
                    </Nav>
                    <Form className="d-flex">
                        <FormControl
                            type="text"
                            placeholder="Search"
                            className="mr-2"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                        <Button variant="outline-light" onClick={handleSearch}>
                            Search
                        </Button>
                    </Form>
                </Navbar.Collapse>
                <Navbar.Text>
                    Usuario: <a href="#login">Iniciar sesión</a>
                </Navbar.Text>
            </Container>
        </Navbar>
    );
};

export default NavbarMenu;