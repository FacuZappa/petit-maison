import { useState, useEffect } from 'react';
import './Navbar.css';

// Pon tu logo en src/assets/ (ej: logo.png o logo.svg) y cambia la ruta abajo
import logoImg from '../../assets/img/logo.png';

const NAV_ITEMS = [
  { label: 'Servicios', href: '#servicios' },
  { label: 'Sobre nosotros', href: '#sobre-nosotros' },
  { label: 'Citas', href: '#citas' },
  { label: 'Portafolio', href: '#portafolio' },
  { label: 'Contacto', href: '#contacto' },
] as const;

const MOBILE_BREAKPOINT_PX = 768;

export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const closeMenu = () => setIsMenuOpen(false);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeMenu();
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= MOBILE_BREAKPOINT_PX) closeMenu();
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <header className="navbar-header">
      <a href="#" className="navbar-logo" onClick={closeMenu} aria-label="Inicio">
        <img src={logoImg} alt="Inicio" className="navbar-logo-img" />
      </a>

      <button
        type="button"
        className="navbar-hamburger"
        onClick={() => setIsMenuOpen((prev) => !prev)}
        aria-expanded={isMenuOpen}
        aria-controls="main-nav"
        aria-label={isMenuOpen ? 'Cerrar menú' : 'Abrir menú'}
      >
        <span className="navbar-hamburger-bar" aria-hidden />
        <span className="navbar-hamburger-bar" aria-hidden />
        <span className="navbar-hamburger-bar" aria-hidden />
      </button>

      <nav id="main-nav" className={`navbar-nav ${isMenuOpen ? 'navbar-nav--open' : ''}`}>
        <ul className="navbar-list">
          {NAV_ITEMS.map(({ label, href }) => (
            <li key={href}>
              <a href={href} className="navbar-link" onClick={closeMenu}>
                {label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
