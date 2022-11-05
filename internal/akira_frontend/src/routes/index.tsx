import { Navigate, RouteObject } from "react-router-dom";
import { MainLayout } from "../layouts/MainLayout";
import { HomeDashboard } from "../pages/HomeDashboard";
import { Projects } from "../pages/Projects";
import { ProjectsCreate } from "../pages/Projects/Create";
import { ProjectsEdit } from "../pages/Projects/Edit";
import { ProjectsDetails } from "../pages/Projects/details";
import { Services } from "../pages/Services";
import { Controller } from "../pages/Controller";

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
