import { Link, useMatch, useResolvedPath } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="nav">
      <Link to="/" className="site-title">
        Парсер ЦИК
      </Link>
      <ul>
        <CustomLink to="/President">Президентские выборы</CustomLink>
        <CustomLink to="/Parliament">Выборы ГосДумы</CustomLink>
        <CustomLink to="/Region">Региональные Выборы</CustomLink>
        <CustomLink to="/ConstRF">Поправки в Конституции РФ</CustomLink>
      </ul>
    </nav>
  );
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to);
  const isActive = useMatch({ path: resolvedPath.pathname, end: true });

  return (
    <li className={isActive ? "active" : ""}>
      <Link to={to} {...props}>
        {children}
      </Link>
    </li>
  );
}
