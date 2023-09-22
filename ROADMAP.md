1. **Environment Setup(Changed to loading from config.json file)**

   - Load environment variables ✅

2. **Testing Framework**

   - Set up testing infrastructure ✅
   - Write unit tests for core functionalities
   - Write integration tests for end-to-end flows
   - Automate testing via CI/CD

3. **Mock Data & Conversations**

   - Use mock data for testing and development ✅
   - Save test conversations to JSON file in `test_data` folder ✅

4. **Output Management**

   - Allow code string copying from output ✅
   - Number code strings for easy copying or running ✅
   - Stream output to the console in real-time ✅
   - Support markdown formatting in output ✅

5. **User Interactivity**

   - Enable continuation of conversations ✅
   - Utilize numerical inputs for quick actions like copying to clipboard ✅
   - Implement special symbols (e.g., `/`, `@`) for calling commands
     - Switch between conversations
     - Start new conversation
     - Get back to the latest conversation
     - Conversation history to Markdown
   - Prompts colors for user and Assistant

6. **API & Model Configuration**

   - Allow setting of API key through the tool's interface ✅
   - Add CLI help option ✅
   - Add `--model` option with auto-completion or interactive display ✅
   - Extend configuration
     - setup systems promts
     - model configs such as temperature and so on

7. **Input Methods**

   - Accept input from a file
   - Accept output from another command as input
   - Allow pasting of data ✅
   - Support URL inputs

8. **Conversation History**

   - send whole conversation history each time ✅
   - Save history to a JSON file ✅
   - Implement fuzzy search over history
   - Decide on best storage model for history (e.g., flat file, database)
   - Allow setting of global path for history storage

9. **User Experience (UX) Improvements**

   - Support command auto-completion
     - Commands:
       - :save - saves history
       - :new - start new conversation
       - :info - prints config info
       - :delete last prompt
       - :help

10. **Interrupt Functionality**

    - Allow interruption of output

11. **Tokens management**

- Price counter and tokens counter
  - conversation price
  - tokens in a conversation
- show what's the short memory size of a model, and how full it is

12. **Add logging**

13. **Add speech to text and text to speech support**
