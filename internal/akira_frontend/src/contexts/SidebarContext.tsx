import React, {
  Dispatch,
  createContext,
  SetStateAction,
  useContext,
  useState,
} from "react";

const sidebarOpenedContext = createContext<boolean>(false);
const setSidebarOpenedContext = createContext<
  Dispatch<SetStateAction<boolean>>
>(() => undefined);

export function useSidebarValue() {
  return useContext(sidebarOpenedContext);
}
export function useSidebarSetValue() {
  return useContext(setSidebarOpenedContext);
}

export function SidebarOpenedProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarOpened, setSidebarOpened] = useState<boolean>(false);

  return (
    <sidebarOpenedContext.Provider value={sidebarOpened}>
      <setSidebarOpenedContext.Provider value={setSidebarOpened}>
        {children}
      </setSidebarOpenedContext.Provider>
    </sidebarOpenedContext.Provider>
  );
}
