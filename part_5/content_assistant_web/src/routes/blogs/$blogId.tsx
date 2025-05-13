import { createFileRoute } from '@tanstack/react-router';
import { blogQueryOptions } from '../../services/blog_postsQueryOptions';
import { useSuspenseQuery } from '@tanstack/react-query';
import Markdown from 'react-markdown';

export const Route = createFileRoute('/blogs/$blogId')({
  component: RouteComponent,
  // @ts-ignore
  loader: ({ context: { queryClient }, params: { blogId } }) => {
    return queryClient.ensureQueryData(blogQueryOptions(blogId));
  },
});

function RouteComponent() {
  const blogId = Route.useParams().blogId;
  const { data: blog } = useSuspenseQuery(blogQueryOptions(blogId));
  return (
    <div className="container mx-auto w-3xl">
      <div className="text-center mt-6 text-3xl font-bold">
        <h1>{blog.title}</h1>
      </div>
      <div className="w-full flex justify-center">
        <img
          src={blog.image_url}
          alt="image related to content"
          className="my-6 object-fill max-h-96 h-auto w-full"
        />
      </div>
      <Markdown
        components={{
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold my-2">{children}</h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-2xl font-semibold my-2">{children}</h2>
          ),
          p: ({ children }) => (
            <p className="text-base/normal my-2">{children}</p>
          ),
        }}
      >
        {blog.content}
      </Markdown>
    </div>
  );
}
