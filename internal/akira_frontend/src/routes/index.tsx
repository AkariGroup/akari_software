import { Navigate, RouteObject } from "react-router-dom";
import { MainLayout } from "../layouts/MainLayout";
import { HomeDashboard } from "../pages/HomeDashboard";

export const AppRoute: RouteObject = {
    path: "",
    element: <MainLayout />,
    children: [
        {
            path: "/",
            element: <HomeDashboard />,
        },
        {
            path: "*",
            element: <Navigate to="/" />,
        }
    ],
};