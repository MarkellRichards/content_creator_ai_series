import axios from "axios"
import config from "../config";

type UUID = string;

export type BlogType = {
    id: number;
    guid: UUID;
    title: string;
    content: string;
    workflow_guid: UUID;
    created_at: Date;
    updated_at: Date;
    image_url: string;
}

export type Blogs = {
  total: number;
  blogs: [BlogType]
}


export const fetchBlogs = async (offset = 0, limit = 10) => {
    console.info('Fetching blogs...')
    return axios
      .get<Blogs>(`${config.CONTENT_SERVER_URL}/blogs`, {
        params: {
          offset,
          limit
        }
      })
      .then((r) => r.data)
  }

export const fetchBlog = async (blog_guid: string) => {
    console.info('Fetching blogs...')
    return axios
      .get<BlogType>(`${config.CONTENT_SERVER_URL}/blog`, {
        params: {
          blog_guid
        }
      })
      .then(r => r.data)
  }