import { Navigate, RouteObject } from "react-router-dom";
import { MainLayout } from "../layouts/MainLayout";
import { Projects } from "../pages/Projects";
import { ProjectsCreate } from "../pages/Projects/Create";
import { ProjectsEdit } from "../pages/Projects/Edit";
import { ProjectsDetails } from "../pages/Projects/details";
import { Services } from "../pages/Services";
import { Controller } from "../pages/Controller";
import { Logs } from "../pages/Services/logs";

export const AppRoute: RouteObject = {
  path: "",
  element: <MainLayout />,
  children: [
    {
      path: "",
      element: <Navigate to="/projects" />,
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
          path: "edit",
          element: <ProjectsEdit />,
        },
        {
          path: "details",
          element: <ProjectsDetails />,
        },
      ],
    },
    {
      path: "/services",
      children: [
        {
          path: "",
          element: <Services />,
        },
        {
          path: "logs/:id",
          element: <Logs />,
        },
      ],
    },
    {
      path: "*",
      element: <Navigate to="/" />,
    },
    {
      path: "/controller",
      element: <Controller />,
    },
  ],
};
