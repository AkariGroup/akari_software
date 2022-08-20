import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

export function CancelButton() {
  const navigate = useNavigate();
  const prevPage = () => {
    navigate(-1);
  };
  return (
    <Button type="button" color="error" variant="outlined" onClick={prevPage}>
      キャンセル
    </Button>
  );
}
