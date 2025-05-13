import { createFileRoute } from '@tanstack/react-router';
import { socialMediaPostQueryOptions } from '../../services/social_mediaQueryOptions';
import { useSuspenseQuery } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';

export const Route = createFileRoute('/social_media/$social_mediaId')({
  component: RouteComponent,
  //@ts-ignore
  loader: ({ context: { queryClient }, params: { social_mediaId } }) => {
    return queryClient.ensureQueryData(
      socialMediaPostQueryOptions(social_mediaId),
    );
  },
});

function RouteComponent() {
  const sm_id = Route.useParams().social_mediaId;
  const { data: sm_data } = useSuspenseQuery(
    socialMediaPostQueryOptions(sm_id),
  );
  const platform =
    sm_data.platform_type[0] + sm_data.platform_type.slice(1).toLowerCase();
  return (
    <div className="container mx-auto w-3xl">
      <img
        src={sm_data.image_url}
        className="my-6 object-fill max-h-96 h-auto w-full"
      />
      <div className="mb-4">
        Platform:
        <span className="text-base ml-1">{platform}</span>
      </div>
      <hr />
      <ReactMarkdown
        components={{
          p: ({ children }) => (
            <p className="text-base/normal py-3">{children}</p>
          ),
          li: ({ children }) => (
            <li className="text-base/normal py-2">{children}</li>
          ),
        }}
      >
        {sm_data.content}
      </ReactMarkdown>
    </div>
  );
}
