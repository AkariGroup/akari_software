import { Box, useTheme } from "@mui/material";
import { Outlet } from "react-router-dom";
import { Header, HeaderHeight } from "./Header";
import { Sidebar, SidebarWidth } from "./Sidebar";

export function MainLayout() {
  const theme = useTheme();
  return (
    <>
      <Sidebar />
      <Header />
      <Box
        sx={{
          display: "block",
          pt: `${HeaderHeight}px`,
          [theme.breakpoints.up("lg")]: {
            ml: `${SidebarWidth}px`,
          },
        }}
      >
        <Outlet />
      </Box>
    </>
  );
}
