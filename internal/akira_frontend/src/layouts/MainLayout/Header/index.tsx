import {
  AppBar as MuiAppBar,
  Box,
  IconButton,
  styled,
  Toolbar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useCallback } from "react";
import { SidebarWidth } from "../Sidebar";
import { useSidebarSetValue } from "../../../contexts/SidebarContext";

export const HeaderHeight = 64;

const AppBar = styled(MuiAppBar)(({ theme }) => ({
  height: HeaderHeight,
  [theme.breakpoints.up("lg")]: {
    left: `${SidebarWidth}px`,
    width: "auto",
  },
}));

export function Header() {
  const setSidebar = useSidebarSetValue();

  const toggleSidebar = useCallback(() => {
    setSidebar((prev) => !prev);
  }, [setSidebar]);

  return (
    <Box sx={{ flexGlow: 1 }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            sx={{
              marginRight: "36px",
              display: {
                lg: "none",
              },
            }}
            onClick={toggleSidebar}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Akari Web Console
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
