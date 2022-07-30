import { Navigate, RouteObject } from "react-router-dom";
import { MainLayout } from "../layouts/MainLayout";
import { HomeDashboard } from "../pages/HomeDashboard";
import { Projects } from "../pages/Projects";
import { ProjectsCreate } from "../pages/Projects/Create";
import { ProjectsDetails } from "../pages/Projects/details";

export const AppRoute: RouteObject = {
  path: "",
  element: <MainLayout />,
  children: [
    {
      path: "",
      element: <HomeDashboard />,
    },
    {
      path: "/projects",
      children: [
        {
          path: "",
          element: <Projects />,
        },
        {
          path: "create",
          element: <ProjectsCreate />,
        },
        {
          path: "details",
          element: <ProjectsDetails />,
        },
      ],
    },
    {
      path: "*",
      element: <Navigate to="/" />,
    },
  ],
};
