import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { App } from "./App";
import { BrowserRouter } from "react-router-dom";
import { SidebarOpenedProvider } from "./contexts/SidebarContext";
import { DarkModeProvider } from "./contexts/DarkmodeContext";
import { BackdropProvider } from "./contexts/BackdropContext";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <DarkModeProvider>
      <SidebarOpenedProvider>
        <BackdropProvider>
          <BrowserRouter basename="/ui">
            <App />
          </BrowserRouter>
        </BackdropProvider>
      </SidebarOpenedProvider>
    </DarkModeProvider>
  </React.StrictMode>
);
