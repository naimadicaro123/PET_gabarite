import { Link } from "react-router-dom";
import '../assets/navbar.css';

export default function Navbar() {
    return (
        <>
            <nav className="navbar">
                <header>
                    <div>
                        <img src="/oci-logo-horizontal-color.svg" alt=""/>
                    </div>
                </header>
                <div className="links">
                        <Link to="/">Inicio</Link>
                        <Link to="/participantes">participantes</Link> 
                        <Link to="/gabaritos">gabaritos</Link>
                </div>
            </nav>
        </>
    )
}