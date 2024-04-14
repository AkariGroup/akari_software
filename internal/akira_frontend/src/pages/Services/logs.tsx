import useAspidaSWR from "@aspida/swr";
import { Box, IconButton, Stack, TextField, Typography } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { NavLink, useParams } from "react-router-dom";
import { useApiClient } from "../../hooks/api";

interface RouteParams {
  id: string;
}

export function Logs() {
  const params = useParams<keyof RouteParams>();
  const client = useApiClient();
  const { data } = useAspidaSWR(client?.services._id(params.id ?? "").logs, {
    enabled: !!client && !!params.id,
  });
  return (
    <Box margin="1em 2em">
      <Box>
        <IconButton
          type="button"
          component={NavLink}
          to="/services"
          size="large"
        >
          <ArrowBackIcon />
        </IconButton>
      </Box>
      <Stack margin={1}>
        <Typography variant="h5" mb={1}>
          サービスログ: {params.id}
        </Typography>
        <Typography variant="h6">Operation Logs</Typography>
        <TextField
          sx={{ padding: 0 }}
          aria-label="Logs"
          minRows={3}
          value={data?.logs}
          variant="filled"
          inputProps={{ readOnly: true }}
          multiline
        />
        <Typography variant="h6">Standard Out</Typography>
        <TextField
          aria-label="Standard Out"
          minRows={3}
          value={data?.stdout}
          variant="filled"
          inputProps={{ readOnly: true }}
          multiline
        />
        <Typography variant="h6">Standard Error</Typography>
        <TextField
          aria-label="Standard Error"
          minRows={3}
          value={data?.stderr}
          variant="filled"
          inputProps={{ readOnly: true }}
          multiline
        />
      </Stack>
    </Box>
  );
}
