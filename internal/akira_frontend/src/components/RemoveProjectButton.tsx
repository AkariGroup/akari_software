import { useCallback, useState } from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import { RemoveDialog, RemoveDialogResult } from "./ProjectCard/removeDialog";
import { Akira_protoProject } from "../api/@types";
import { IconButton } from "@mui/material";

type RemoveButtonProps = {
  project: Akira_protoProject;
  onRemove: (target: Akira_protoProject) => void;
};


const onRemoveProject = useCallback(
  async (target: Akira_protoProject) => {
    if (!client || !target.id) return;

    setBusy(true);
    try {
      await client.projects._id(target.id).remove.post();
      mutate?.();
    } finally {
      setBusy(false);
    }
  },
  [client, setBusy, mutate]
);

export function RemoveButton(props: RemoveButtonProps) {
  const [opened, setOpened] = useState(false);
  const onConfirm = useCallback(
    (d: RemoveDialogResult) => {
      setOpened(false);
      if (d === RemoveDialogResult.CANCEL) {
        return;
      } else {
        props.onRemove(props.project);
      }
    },
    [props, setOpened]
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