import { useEffect, useRef, useState } from 'react';
import { createFileRoute, useNavigate } from '@tanstack/react-router';
import config from '../../config';

interface UserMessage {
  topic: string;
  research: boolean;
}

interface ServerMessage {
  type: string;
  payload: string;
}

type Message = UserMessage | ServerMessage;

export const Route = createFileRoute('/workflows/create')({
  component: RouteComponent,
});

function RouteComponent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputTopic, setInputTopic] = useState<string>('');
  const [inputResearch, setInputResearch] = useState<boolean>(false);
  const [inputVisible, setIsVisible] = useState<boolean>(true);

  const ws = useRef<WebSocket | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    ws.current = new WebSocket(`${config.CONTENT_SERVER_WS}/content`);

    ws.current.onopen = () => {
      console.log('Connected to WebSocket server');
    };

    ws.current.onmessage = (event) => {
      try {
        const serverMessage: ServerMessage = JSON.parse(event.data);
        setMessages((prevMessages) => [...prevMessages, serverMessage]);

        if (serverMessage.type === 'results') {
          if (serverMessage.payload !== 'Failed') {
            const workflowGuid = serverMessage.payload;
            setTimeout(() => {
              navigate({ to: `/workflows/${workflowGuid}` });
            }, 5000);
          } else {
            alert('The workflow has failed. We are looking into issue.');
          }
        } else if (serverMessage.type === 'error') {
        }
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current.onclose = () => {
      console.log('Disconnected from WebSocket server');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [navigate]);

  const sendMessage = () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      const userMessage: UserMessage = {
        topic: inputTopic,
        research: inputResearch,
      };
      ws.current.send(JSON.stringify(userMessage));
      setMessages([...messages, userMessage]);
      setInputTopic('');
      setIsVisible(false);
    }
  };

  return (
    <div className="flex h-screen w-screen justify-center items-center px-4 py-6 flex-col">
      <h2 className="text-2xl font-bold mb-4">Content Generation Workflow</h2>
      <div className="mb-4 w-full max-w-md mx-auto">
        <ul className="list-none p-0">
          {messages.map((msg, index) => {
            if ('topic' in msg) {
              return (
                <li
                  key={index}
                  className="mb-4 p-4 rounded-lg shadow-md bg-gray-50 border-l-4 border-violet-500"
                >
                  <p className="text-lg font-semibold">Topic: {msg.topic}</p>
                </li>
              );
            } else {
              return (
                <li
                  key={index}
                  className="mb-4 p-4 rounded-lg shadow-md bg-gray-200"
                >
                  {msg.type === 'progress_event' ? (
                    <p className="font-semibold text-violet-500">
                      Step: {msg.payload}
                    </p>
                  ) : msg.type === 'error' ? (
                    <p className="font-semibold text-violet-500">
                      {msg.type}: {msg.payload}
                    </p>
                  ) : (
                    <p className="font-semibold text-violet-500">
                      Workflow complete
                    </p>
                  )}
                </li>
              );
            }
          })}
        </ul>
      </div>
      {inputVisible && (
        <div className="flex flex-col w-full max-w-md mx-auto">
          <input
            type="text"
            value={inputTopic}
            onChange={(e) => setInputTopic(e.target.value)}
            className="border border-gray-300 p-3 rounded shadow-sm mb-4 focus:border-violet-500 focus:ring focus:ring-violet-200 focus:outline-none"
            placeholder="Type a research topic"
          />
          <div className="mb-4 flex flex-col">
            <div className="flex items-center mb-1">
              <input
                type="checkbox"
                checked={inputResearch}
                onChange={(e) => setInputResearch(e.target.checked)}
                className="form-checkbox h-5 w-5 text-violet-600"
              />
              <label className="ml-2 text-gray-700">Research</label>
            </div>
            <span className="text-xs text-gray-500 ml-7">
              This will source information from the internet to enhance the
              generation quality.
              {/* (<Link to="/usage-fees" className="underline">see usage fees</a>) - does not exist yet. Future iteration */}
            </span>
          </div>
          <button
            onClick={sendMessage}
            className="bg-violet-500 hover:bg-violet-700 text-white font-bold py-2 px-4 rounded shadow transition duration-300 ease-in-out transform hover:scale-105"
          >
            Send
          </button>
        </div>
      )}
    </div>
  );
}
