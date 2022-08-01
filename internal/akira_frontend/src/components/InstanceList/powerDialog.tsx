import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

export enum DialogResult {
  CANCEL = 0,
  SHUTDOWN = 1,
  TERMINATE = 2,
}

type Props = {
  onResponse: (d: DialogResult) => void;
};

export function PowerDialog(props: Props) {
  return (
    <Dialog open={true} onClose={() => props.onResponse(DialogResult.CANCEL)}>
      <DialogTitle>シャットダウンしますか</DialogTitle>
      <DialogContent>
        <DialogContentText>Terminate option</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => props.onResponse(DialogResult.CANCEL)}>
          キャンセル
        </Button>
        <Button
          onClick={() => props.onResponse(DialogResult.SHUTDOWN)}
          color="error"
        >
          停止
        </Button>
        <Button
          onClick={() => props.onResponse(DialogResult.TERMINATE)}
          color="error"
        >
          完全停止
        </Button>
      </DialogActions>
    </Dialog>
  );
}
