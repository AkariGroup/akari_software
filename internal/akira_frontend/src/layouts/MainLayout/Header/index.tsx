import {
  AppBar as MuiAppBar,
  Badge,
  Box,
  IconButton,
  Menu,
  MenuItem,
  styled,
  Toolbar,
  Tooltip,
  Typography,
  useTheme,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useCallback, useState } from "react";
import AccountCircle from "@mui/icons-material/AccountCircle";
import NotificationsIcon from "@mui/icons-material/Notifications";
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
  const theme = useTheme();
  const [anchorElAvatar, setAnchorElAvatar] = useState<HTMLElement | null>(
    null
  );

  const handleAvatarClick: React.MouseEventHandler<HTMLButtonElement> =
    useCallback((e) => {
      setAnchorElAvatar(e.currentTarget);
    }, []);
  const closeAvatarMenu = useCallback(() => {
    setAnchorElAvatar(null);
  }, []);
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

          <Box sx={{ flexGrow: 0 }}>
            <IconButton size="large" color="inherit">
              <Badge badgeContent={1} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
            <Tooltip title="Open user settings">
              <IconButton
                size="large"
                onClick={handleAvatarClick}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: "45px" }}
              anchorEl={anchorElAvatar}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorElAvatar)}
              onClose={closeAvatarMenu}
            >
              <MenuItem onClick={closeAvatarMenu}>Setup SSH key</MenuItem>
              <MenuItem onClick={closeAvatarMenu}>Log out</MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
