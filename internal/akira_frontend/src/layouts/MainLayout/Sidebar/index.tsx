import {
  Avatar,
  Button,
  Divider,
  Drawer as MuiDrawer,
  FormControlLabel,
  FormGroup,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  styled,
  Switch,
} from "@mui/material";
import { Link, NavLink } from "react-router-dom";
import DashboardIcon from "@mui/icons-material/Dashboard";
import WorkIcon from "@mui/icons-material/Work";
import AppsIcon from "@mui/icons-material/Apps";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import {
  useSidebarSetValue,
  useSidebarValue,
} from "../../../contexts/SidebarContext";
import { useCallback } from "react";
import {
  useDarkmodeValue,
  useSetDarkmodeValue,
} from "../../../contexts/DarkmodeContext";
import { purple } from "@mui/material/colors";

type Props = {};

export const SidebarWidth = 250;

const Drawer = styled(MuiDrawer)(() => ({
  "& .MuiDrawer-paper": {
    width: SidebarWidth,
  },
}));

function SidebarItems() {
  return (
    <List component="nav" sx={{ pt: 0 }}>
      <ListItem
        component="div"
        sx={{
          maxHeight: 64,
          // TODO: Use theme.palette
          backgroundColor: (theme) =>
            theme.palette.mode === "light"
              ? theme.palette.grey[200]
              : purple[400],
        }}
      >
        <Button component={Link} to="/">
          <Avatar
            src="/images/logo.png"
            sx={{ width: 60, height: 60 }}
            variant="rounded"
          />
        </Button>
      </ListItem>
      <ListItemButton component={NavLink} to="/">
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Dashboard" />
      </ListItemButton>
      <ListItemButton component={NavLink} to="/projects">
        <ListItemIcon>
          {" "}
          <WorkIcon />
        </ListItemIcon>
        <ListItemText primary="Projects" />
      </ListItemButton>
      <ListItemButton component={NavLink} to="/services">
        <ListItemIcon>
          <AppsIcon />
        </ListItemIcon>
        <ListItemText primary="Services" />
      </ListItemButton>
      <ListItemButton component={NavLink} to="/controller">
        <ListItemIcon>
          <SportsEsportsIcon />
        </ListItemIcon>
        <ListItemText primary="Controller" />
      </ListItemButton>
    </List>
  );
}

function DarkModeToggleButton() {
  const darkmode = useDarkmodeValue();
  const setDarkmode = useSetDarkmodeValue();
  const handleDarkmodeChange = useCallback(
    (_: any, checked: boolean) => {
      setDarkmode(checked);
    },
    [setDarkmode]
  );

  return (
    <List sx={{ marginTop: "auto", pb: 0 }}>
      <Divider />
      <ListItem
        sx={{
          backgroundColor: (theme) =>
            theme.palette.mode === "light"
              ? theme.palette.grey[200]
              : theme.palette.grey[900],
        }}
      >
        <FormGroup>
          <FormControlLabel
            control={
              <Switch
                color="secondary"
                checked={darkmode}
                onChange={handleDarkmodeChange}
              />
            }
            label="&nbsp;Dark Mode"
          />
        </FormGroup>
      </ListItem>
    </List>
  );
}

export function Sidebar(props: Props) {
  const opened = useSidebarValue();
  const setOpened = useSidebarSetValue();
  const handleClose = useCallback(() => {
    setOpened(false);
  }, [setOpened]);

  const darkMode = <DarkModeToggleButton />;
  return (
    <>
      <Drawer
        variant="permanent"
        anchor="left"
        sx={{
          display: {
            xs: "none",
            lg: "block",
          },
        }}
      >
        <SidebarItems />
        {darkMode}
      </Drawer>
      <Drawer
        variant="temporary"
        anchor="left"
        elevation={10}
        open={opened}
        onClose={handleClose}
      >
        <SidebarItems />
        {darkMode}
      </Drawer>
    </>
  );
}
