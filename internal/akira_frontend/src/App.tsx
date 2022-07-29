import { createTheme, CssBaseline, useTheme } from "@mui/material";
import { ThemeProvider } from "@mui/system";
import { useRoutes } from "react-router-dom";
import { useDarkmodeValue } from "./contexts/DarkmodeContext";
import { AppRoute } from "./routes";

export function App() {
  const content = useRoutes([AppRoute]);
  const darkmode = useDarkmodeValue();
  const theme = createTheme({
    palette: {
      mode: darkmode ? "dark" : "light",
    },
  });
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {content}
    </ThemeProvider>
  );
}
