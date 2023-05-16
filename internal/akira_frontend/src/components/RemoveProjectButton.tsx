import useAspidaSWR from "@aspida/swr";
import { useCallback, useState } from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import { RemoveDialog, RemoveDialogResult } from "./ProjectCard/removeDialog";
import { ApiClient } from "../hooks/api";
import { Akira_protoProject } from "../api/@types";
import { IconButton } from "@mui/material";

type RemoveButtonProps = {
  project: Akira_protoProject;
  client: ApiClient;
  onRemove: (target: Akira_protoProject) => void;
};

export function RemoveButton(props: RemoveButtonProps) {
  const [opened, setOpened] = useState(false);
  const { mutate } = useAspidaSWR(props.client?.projects, {
    enabled: !!props.client,
  });
  const onConfirm = useCallback(
    async (d: RemoveDialogResult) => {
      setOpened(false);
      if (d === RemoveDialogResult.CANCEL) {
        return;
      } else {
        await props.onRemove(props.project);
        await props.client.projects.refresh.post({
          body: {},
        });
        mutate();
      }
    },
    [props, mutate, setOpened]
  );
  return (
    <>
      {opened ? (
        <RemoveDialog
          projectName={props.project.manifest?.name ?? ""}
          onResponse={onConfirm}
        />
      ) : null}
      <IconButton onClick={() => setOpened(true)}>
        <DeleteIcon />
      </IconButton>
    </>
  );
}
