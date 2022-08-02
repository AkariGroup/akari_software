import { Button, Menu, MenuItem } from "@mui/material";
import { MouseEventHandler, useCallback, useState } from "react";
import { Akira_protoServiceInstance } from "../api/@types";

type Props = {
  instances?: Akira_protoServiceInstance[];
  onSelected: (s: Akira_protoServiceInstance) => void;
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
    async (s: Akira_protoServiceInstance) => {
      handleClose();
      props.onSelected(s);
    },
    [props, handleClose]
  );

  const runningInstances = props.instances?.filter(
    (s) =>
      s.status === "RUNNING" &&
      s.service?.capabilities?.includes("open_project")
  );
  const hasActiveInstances = (runningInstances?.length ?? 0) > 0;

  return (
    <>
      <Button onClick={handleClick} disabled={!hasActiveInstances}>
        Open With Service
      </Button>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        {runningInstances?.map((s) => (
          <MenuItem key={s.id} onClick={() => onItemClick(s)}>
            {s.displayName}
          </MenuItem>
        ))}
      </Menu>
    </>
  );
}
