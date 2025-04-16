import axios from "axios"
import config from "../config";

type UUID = string;

export type SocialMediaType = {
    id: number;
    guid: UUID;
    content: string;
    platform_type: string; //change to enum
    workflow_guid: UUID;
    created_at: Date;
    updated_at: Date;
    image_url: string;
}

export type SocialMedias = {
  total: number;
  social_media_posts: [SocialMediaType]
}


export const fetchSocialMediaPosts = async (offset: number, limit: number) => {
    console.info('Fetching socialMedia...')
    return axios
      .get<SocialMedias>(`${config.CONTENT_SERVER_URL}/social_media_posts`, {
        params: {
          offset, limit
        }
      })
      .then((r) => r.data)
  }

  export const fetchSocialMediaPost = async (sm_guid: string) => {
    console.info('Fetching socialMedia...')
    return axios
      .get<SocialMediaType>(`${config.CONTENT_SERVER_URL}/social_media_post`, {
        params: {
          sm_guid
        }
      })
      .then(r => r.data)
  }