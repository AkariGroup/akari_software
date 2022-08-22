import {
  Backdrop,
  CircularProgress,
  createTheme,
  CssBaseline,
} from "@mui/material";
import { ThemeProvider } from "@mui/system";
import { useEffect } from "react";
import { useRoutes } from "react-router-dom";
import { useBackdropValue } from "./contexts/BackdropContext";
import {
  useDarkmodeValue,
  DARKMODE_LOCALSTORAGE_KEY,
} from "./contexts/DarkmodeContext";
import { AppRoute } from "./routes";

export function App() {
  const content = useRoutes([AppRoute]);
  const darkmode = useDarkmodeValue();
  useEffect(() => {
    localStorage.setItem(DARKMODE_LOCALSTORAGE_KEY, darkmode ? "on" : "off");
  }, [darkmode]);
  const backdrop = useBackdropValue();
  const theme = createTheme({
    palette: {
      mode: darkmode ? "dark" : "light",
    },
  });
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={backdrop}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
      {content}
    </ThemeProvider>
  );
}
