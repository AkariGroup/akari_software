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
import { grey, purple } from "@mui/material/colors";

type Props = {};

export const SidebarWidth = 250;

const Drawer = styled(MuiDrawer)(() => ({
  "& .MuiDrawer-paper": {
    width: SidebarWidth,
  },
}));
const SidebarListItemButton = styled(ListItemButton)(({ theme }) => ({
  "&.active": {
    background: theme.palette.mode === "dark" ? grey[800] : grey[300],
  },
})) as typeof ListItemButton;

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
      <SidebarListItemButton component={NavLink} to="/projects">
        <ListItemIcon>
          {" "}
          <WorkIcon />
        </ListItemIcon>
        <ListItemText primary="Projects" />
      </SidebarListItemButton>
      <SidebarListItemButton component={NavLink} to="/services">
        <ListItemIcon>
          <AppsIcon />
        </ListItemIcon>
        <ListItemText primary="Services" />
      </SidebarListItemButton>
      <SidebarListItemButton component={NavLink} to="/controller">
        <ListItemIcon>
          <SportsEsportsIcon />
        </ListItemIcon>
        <ListItemText primary="Controller" />
      </SidebarListItemButton>
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
