import { queryOptions } from "@tanstack/react-query";
import { fetchBlogs, fetchBlog } from "./blog_posts";


export const blogsQueryOptions = (offset: number, limit: number) => queryOptions({
    queryKey: ['blogs', {offset}, {limit}],
    queryFn: () => fetchBlogs(offset, limit),
});

export const blogQueryOptions = (blog_guid: string) => queryOptions({
    queryKey: ['blog', {blog_guid}],
    queryFn: () => fetchBlog(blog_guid)
})