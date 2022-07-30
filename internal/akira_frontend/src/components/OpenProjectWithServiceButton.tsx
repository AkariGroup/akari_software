import useAspidaSWR from "@aspida/swr";
import { Button, Menu, MenuItem } from "@mui/material";
import { MouseEventHandler, useCallback, useState } from "react";
import { useApiClient } from "../hooks/api";

export function OpenProjectWithServiceButton() {
  const client = useApiClient();
  const { data } = useAspidaSWR(client.instances, {
    enabled: !!client,
  });

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

  if (!data) {
    return <></>;
  }

  const runningInstances = data.instances?.filter(s => s.status === "RUNNING");
  const hasActiveInstances = (runningInstances?.length ?? 0) > 0;

  return (
    <>
      <Button onClick={handleClick} disabled={!hasActiveInstances}>Open With Service</Button>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)}>
        {data?.instances?.map((s) => {
          if (s.status !== "RUNNING") {
            return null;
          }
          return <MenuItem onClick={handleClose}>{s.displayName}</MenuItem>;
        })}
      </Menu>
    </>
  );
}
