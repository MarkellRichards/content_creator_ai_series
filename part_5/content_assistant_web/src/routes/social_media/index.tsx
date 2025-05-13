import { createFileRoute, Outlet } from '@tanstack/react-router';
import { socialMediaPostsQueryOptions } from '../../services/social_mediaQueryOptions';
import { useSuspenseQuery } from '@tanstack/react-query';
import { useState } from 'react';
import Pagination from '../../components/pagination/pagination';
import SocialMediaCard from '../../components/social_media/social_media';

export const Route = createFileRoute('/social_media/')({
  component: RouteComponent,
  //@ts-ignore
  loader: ({ context: { queryClient }, params: { offset, limit } }) =>
    queryClient.ensureQueryData(socialMediaPostsQueryOptions(offset, limit)),
});

function RouteComponent() {
  const [offset, setOffset] = useState(0);
  const LIMIT = 5;
  const socialMediaPostsQuery = useSuspenseQuery(
    socialMediaPostsQueryOptions(offset, LIMIT),
  );
  const socialMediaPosts = socialMediaPostsQuery.data.social_media_posts;
  const total = socialMediaPostsQuery.data.total;

  return (
    <div className="my-8 flex flex-col container mx-auto">
      <div className="mb-8 text-center text-2xl font-bold">
        Your Social Media Posts
      </div>
      <ul className="grid lg:grid-cols-4 sm:grid-cols-1 gap-8 container mx-auto">
        {[...socialMediaPosts].map((sm) => {
          return (
            <li key={sm.id} className="whitespace-nowrap">
              <SocialMediaCard social_media={sm} />
            </li>
          );
        })}
      </ul>
      <Pagination
        total={total}
        offset={offset}
        limit={LIMIT}
        setOffset={setOffset}
      />
      <Outlet />
    </div>
  );
}
