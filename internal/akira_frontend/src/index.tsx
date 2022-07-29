import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { App } from "./App";
import { BrowserRouter } from "react-router-dom";
import { SidebarOpenedProvider } from "./contexts/SidebarContext";
import { DarkModeProvider } from "./contexts/DarkmodeContext";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <DarkModeProvider>
      <SidebarOpenedProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </SidebarOpenedProvider>
    </DarkModeProvider>
  </React.StrictMode>
);
