import {
  Box,
  Card as MuiCard,
  CardActionArea,
  CardActions,
  CardContent,
  Divider,
  IconButton,
  styled,
  Typography,
} from "@mui/material";
import { Akira_protoProject } from "../../api/@types";
import { RemoveButton } from "../RemoveProjectButton";
import LaunchIcon from "@mui/icons-material/Launch";
import AddCircleOutlineOutlinedIcon from "@mui/icons-material/AddCircleOutlineOutlined";
import { Link } from "react-router-dom";

const ProjectCardHeight = 200;
const ProjectCardWidth = 250;

const SizeLimitedTypography = styled(Typography)({
  display: "block",
  overflow: "hidden",
  textOverflow: "ellipsis",
  overflowWrap: "break-word",
});

const Card = styled(MuiCard)({
  width: ProjectCardWidth,
  height: ProjectCardHeight,
});

type Prop = {
  project: Akira_protoProject;
  onRemove: (target: Akira_protoProject) => void;
};

export function NewProjectButtonCard() {
  return (
    <Card>
      <CardActionArea
        component={Link}
        to="/projects/create"
        sx={{ display: "flex", height: "100%", flexDirection: "column" }}
      >
        <Box
          sx={{
            display: "flex",
            margin: "0 auto",
            justifyContent: "center",
            alignItems: "center",
            height: "70%",
          }}
        >
          <AddCircleOutlineOutlinedIcon fontSize="large" color="primary" />
        </Box>
        <Divider />
        <Typography variant="h5" textAlign="center" sx={{ mt: 1 }}>
          新規プロジェクト
        </Typography>
      </CardActionArea>
    </Card>
  );
}

export function ProjectCard({ project, onRemove }: Prop) {
  return (
    <Card>
      <Box sx={{ display: "flex", height: "100%", flexDirection: "column" }}>
        <CardActionArea
          component={Link}
          to={`/projects/details?id=${project.id}`}
          sx={{ height: "100%" }}
        >
          <CardContent sx={{ width: "100%" }}>
            <SizeLimitedTypography variant="h5" sx={{ whiteSpace: "nowrap" }}>
              {project.manifest?.name}
            </SizeLimitedTypography>
            <SizeLimitedTypography
              variant="body2"
              sx={{ whiteSpace: "nowrap" }}
            >
              {project.manifest?.author}
            </SizeLimitedTypography>
            <Typography
              variant="body2"
              color="text.secondary"
              textOverflow="ellipsis"
              sx={{
                mt: 1,
                "-webkit-box-orient": "vertical",
                "-webkit-line-clamp": "6",
                display: "-webkit-box",
                overflow: "hidden",
                overflowWrap: "break-word",
                textOverflow: "ellipsis",
              }}
            >
              {project.manifest?.description}
            </Typography>
          </CardContent>
        </CardActionArea>
        <CardActions
          sx={{
            display: "flex",
            width: "100%",
            alignItems: "flex-end",
            flex: "1 0 auto",
          }}
          disableSpacing
        >
          <IconButton component={Link} to="/services">
            <LaunchIcon />
          </IconButton>
          <RemoveButton project={project} onRemove={onRemove} />
        </CardActions>
      </Box>
    </Card>
  );
}
