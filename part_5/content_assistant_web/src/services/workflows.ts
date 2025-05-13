import axios from "axios"
import { BlogType } from "./blog_posts";
import { SocialMediaType } from "./social_media_posts";
import config from "../config";

export type WorkflowStatus = "COMPLETE" | "FAILED" | "INPROGRESS"

type UUID = string;

export type WorkflowType = {
    id: number;
    guid: UUID;
    status: WorkflowStatus;
    created_at: Date;
    updated_at: Date; 
}

export type Workflows = {
  total: number;
  workflows: [WorkflowType]
}

export type WorkflowAggregate = {
  workflow: WorkflowType;
  blog_posts:BlogType[];
  social_media_posts: SocialMediaType[]
}

export type FilterCriteria = {
  status: WorkflowStatus
}

export const fetchWorkflows = async (offset: number, limit: number, filter_criteria?: WorkflowStatus ) => {
    const payload = {
      offset, 
      limit,
      filter_criteria: filter_criteria
    };
    return axios
      .post<Workflows>(`${config.CONTENT_SERVER_URL}/workflows`, payload)
      .then((r) => r.data)
    
  }

  export const fetchWorkflow = async (workflow_guid: string) => {
      const response = await axios
        .get<WorkflowAggregate>(`${config.CONTENT_SERVER_URL}/workflow`, {
          params: {
            workflow_guid
          }
        })
        console.log(response.data)
        return response.data
    
  }