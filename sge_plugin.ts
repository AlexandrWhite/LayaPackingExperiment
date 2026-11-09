import { Plugin } from "@opencode/plugin";

const prompt1 = (problem: string) =>
  "You are an expert in optimization algorithms. \
List heuristics or methods that can solve the " + problem + ". \
Provide the methods in a JSON array format. \
Ensure the response is valid JSON, and nothing else. \
For example: [\"Method1\", \"Method2\", \"Method3\"]";

const greeting = (name: string) => `${name}! Plugin successfully works`;

export default Plugin.define({
  id: "sge",
  async setup(ctx) {
    await ctx.tool.transform((editor) => {
      editor.add({
        name: "sge",
        description: "Solve combinatorial problem using Self-Guiding Exploration",
        input: {
          type: "object",
          properties: {
            name: { type: "string" },
          },
          required: ["name"],
          additionalProperties: false,
        },
        async execute(input) {
          return {
            content: greeting((input as { name: string }).name),
          };
        },
      });
    });

    await ctx.command.transform((editor) => {
      editor.add({
        name: "sge",
        description: "Solve combinatorial problem using Self-Guiding Exploration",
        async execute({ sessionID, prompt, delivery }) {
          const problem = prompt.text.trim();

          if (!problem) {
            await ctx.session.synthetic({
              sessionID,
              text: "Tell me your problem: /sge <problem>",
            });
            return;
          }

         
          // const result2 = await ctx.session.prompt({
          //   ...prompt,
          //   sessionID,
          //   noReply: true,
          //   text: prompt1(problem),
          //   delivery,
          // });
          

          // const result = await ctx.session.prompt({
          //   ...prompt,
          //   sessionID,
          //   text: prompt1(problem),
          //   delivery,
          // });
          
          

          


          // for (const method of methods) {
          //   console.log(method); 
          // }


        },
      });
    });
  },
});
