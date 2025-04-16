import { queryOptions } from "@tanstack/react-query";
import { fetchSocialMediaPost, fetchSocialMediaPosts } from "./social_media_posts";

export const socialMediaPostsQueryOptions = (offset: number, limit:number) => queryOptions({
    queryKey: ['social_media_posts', {offset}, {limit}],
    queryFn: () => fetchSocialMediaPosts(offset, limit)
})

export const socialMediaPostQueryOptions = (sm_guid: string) => queryOptions({
    queryKey: ['social_media', {sm_guid}],
    queryFn: () => fetchSocialMediaPost(sm_guid)
})