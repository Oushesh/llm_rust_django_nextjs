use llm_chain::parameters;
use llm_chain::step::Step;
use llm_chain::traits::Executor as ExecutorTrait;
use llm_chain::{chains::sequential::Chain, prompt};
use llm_chain_openai::chatgpt::Executor;

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create a new ChatGPT executor with the default settings
    let exec = Executor::new()?;

    // Create a chain of steps with two prompts
    let chain: Chain = Chain::new(vec![
        // First step: make a personalized birthday email
        Step::for_prompt_template(
            prompt!("What is the biggest mammal that lays eggs?")
        ),

        // Second step: summarize the email into a tweet. Importantly, the text parameter becomes the result of the previous prompt.
        Step::for_prompt_template(
            prompt!( "You are a bot that generates the reasoning steps", "Summarise the steps and check whether those steps are true or false to finally give an answer on whether the question is legit or not!  \n--\n{{text}}")
        )
    ]);

    // Run the chain with the provided parameters
    let res = chain
        .run(
            // Create a Parameters object with key-value pairs for the placeholders
            parameters!("name" => "Emil", "date" => "February 30th 2023"),
            &exec,
        )
        .await
        .unwrap();

    // Print the result to the console
    println!("{}", res.to_immediate().await?.as_content());
    Ok(())
}