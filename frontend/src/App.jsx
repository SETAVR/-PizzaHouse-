import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
import CartPage from "./pages/CartPage";
import CheckoutPage from "./pages/CheckoutPage";
import FavoritesPage from "./pages/FavoritesPage";
import LoginPage from "./pages/LoginPage";
import MyOrdersPage from "./pages/MyOrdersPage";
import OrderPage from "./pages/OrderPage";
import PizzaDetailPage from "./pages/PizzaDetailPage";
import CatalogPage from "./pages/CatalogPage";
import ProfilePage from "./pages/ProfilePage";
import RegisterPage from "./pages/RegisterPage";

function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) {
    return <main className="container">Загрузка...</main>;
  }
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<CatalogPage />} />
          <Route path="/pizzas/:id" element={<PizzaDetailPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<ProtectedRoute><CheckoutPage /></ProtectedRoute>} />
          <Route path="/orders" element={<ProtectedRoute><MyOrdersPage /></ProtectedRoute>} />
          <Route path="/orders/:id" element={<ProtectedRoute><OrderPage /></ProtectedRoute>} />
          <Route path="/favorites" element={<ProtectedRoute><FavoritesPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </CartProvider>
    </AuthProvider>
  );
}
