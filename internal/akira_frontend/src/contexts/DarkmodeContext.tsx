import React, {
  Dispatch,
  createContext,
  SetStateAction,
  useContext,
} from "react";

export const DARKMODE_LOCALSTORAGE_KEY = "darkmode"
const darkmodeContext = createContext<boolean>(false);
const setDarkmodeContext = createContext<Dispatch<SetStateAction<boolean>>>(
  () => undefined
);

export function useDarkmodeValue() {
  return useContext(darkmodeContext);
}
export function useSetDarkmodeValue() {
  return useContext(setDarkmodeContext);
}

export function DarkModeProvider({ children }: { children: React.ReactNode }) {
  const [darkmode, setDarkmode] = React.useState(() => localStorage.getItem(DARKMODE_LOCALSTORAGE_KEY) === "on");
  return (
    <darkmodeContext.Provider value={darkmode}>
      <setDarkmodeContext.Provider value={setDarkmode}>
        {children}
      </setDarkmodeContext.Provider>
    </darkmodeContext.Provider>
  );
}
