import { Button, Menu, MenuItem } from "@mui/material";
import { MouseEventHandler, useCallback, useState } from "react";
import { Akira_protoService } from "../api/@types";

type Props = {
  services?: Akira_protoService[];
  onSelected: (s: Akira_protoService) => void;
};

export function OpenProjectWithServiceButton(props: Props) {
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const handleClick: MouseEventHandler<HTMLElement> = useCallback(
    (e) => {
      setAnchorEl(e.currentTarget);
    },
    [setAnchorEl]
  );
  const handleClose = useCallback(() => {
    setAnchorEl(null);
  }, [setAnchorEl]);
  const onItemClick = useCallback(
    async (s: Akira_protoService) => {
      handleClose();
      props.onSelected(s);
    },
    [props, handleClose]
  );

  const runningServices = props.services?.filter(
    (s) =>
      s.status === "RUNNING" && s.image?.capabilities?.includes("open_project")
  );
  const hasActiveServices = (runningServices?.length ?? 0) > 0;

  return (
    <>
      <Button onClick={handleClick} disabled={!hasActiveServices}>
        Open With Service
      </Button>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        {runningServices?.map((s) => (
          <MenuItem key={s.id} onClick={() => onItemClick(s)}>
            {s.displayName}
          </MenuItem>
        ))}
      </Menu>
    </>
  );
}
