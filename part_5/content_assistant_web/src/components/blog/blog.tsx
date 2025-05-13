import ReactMarkdown from 'react-markdown';
import { BlogType } from '../../services/blog_posts';
import { Link } from '@tanstack/react-router';

type BlogCardProps = {
  blog: BlogType;
};

const BlogCard: React.FC<BlogCardProps> = ({ blog }) => {
  return (
    <Link to="/blogs/$blogId" params={{ blogId: blog.guid }}>
      <div className="max-w-sm rounded overflow-hidden shadow-lg p-4 bg-white h-full">
        <img
          className="w-full h-48 object-fill"
          src={blog.image_url}
          alt={blog.title}
        />
        <div className="px-6 py-4">
          <div className="font-bold text-xl mb-2">{blog.title}</div>
          <div className="text-gray-700 text-base line-clamp-5">
            <ReactMarkdown>{blog.content}</ReactMarkdown>
          </div>
        </div>
        <div className="px-6 pt-4 pb-2">
          <p className="text-gray-600 text-sm">
            {new Date(blog.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    </Link>
  );
};

export default BlogCard;
