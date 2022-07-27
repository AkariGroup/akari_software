import React, {
  Dispatch,
  createContext,
  SetStateAction,
  useContext,
  useState,
} from "react";

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
  const [darkmode, setDarkmode] = useState<boolean>(false);

  return (
    <darkmodeContext.Provider value={darkmode}>
      <setDarkmodeContext.Provider value={setDarkmode}>
        {children}
      </setDarkmodeContext.Provider>
    </darkmodeContext.Provider>
  );
}
