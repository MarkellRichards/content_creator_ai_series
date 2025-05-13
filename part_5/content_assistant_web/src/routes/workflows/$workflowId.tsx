import { createFileRoute } from '@tanstack/react-router';
import { workflowQueryOptions } from '../../services/workflowsQueryOptions';
import { useSuspenseQuery } from '@tanstack/react-query';
import BlogCard from '../../components/blog/blog';
import SocialMediaCard from '../../components/social_media/social_media';

export const Route = createFileRoute('/workflows/$workflowId')({
  component: RouteComponent,
  // @ts-ignore
  loader: ({ context: { queryClient }, params: { workflowId } }) => {
    return queryClient.ensureQueryData(workflowQueryOptions(workflowId));
  },
});

function RouteComponent() {
  const workflowId = Route.useParams().workflowId;
  const { data: data } = useSuspenseQuery(workflowQueryOptions(workflowId));

  return (
    <div className="container mx-auto">
      <div className="my-8 text-center text-2xl font-bold">
        Workflow: {data.workflow.guid.slice(0, 8)} - {data.workflow.status}
      </div>
      <div>
        <h2 className="text-2xl font-bold">Blog Posts</h2>
        {[...data.blog_posts].map((blog, index) => {
          return <BlogCard key={index} blog={blog}></BlogCard>;
        })}
      </div>
      <br />
      <div>
        <h2 className="text-2xl font-bold">Social Media Posts</h2>
        {[...data.social_media_posts].map((sm_post, index) => {
          return <SocialMediaCard key={index} social_media={sm_post} />;
        })}
      </div>
    </div>
  );
}
