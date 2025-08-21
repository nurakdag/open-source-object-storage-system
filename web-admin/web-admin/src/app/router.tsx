import { createBrowserRouter } from "react-router-dom";
import Layout from "../components/Layout";
import { DashboardPage } from "../pages/DashboardPage";
import ObjectsPage from "../pages/ObjectsPage";
import LoginPage from "../pages/LoginPage";
import AuthGuard from "./authGuard";

export const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  {
    path: "/",
    element: <AuthGuard />,
    children: [
      {
        element: <Layout />,
        children: [
          { index: true, element: <DashboardPage /> },
          { path: "bucket/:name", element: <ObjectsPage /> },
        ],
      },
    ],
  },
]);
