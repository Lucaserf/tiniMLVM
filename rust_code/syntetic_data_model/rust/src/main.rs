
use std::{env,fs,io,error::Error}
use wasi_nn::{GraphBuilder, GraphEncoding, ExecutionTarget, TensorType};


pub fn main() -> Result<(), Box<dyn Error>>{
    let args: Vec<String> = env::args().collect();
    let model_bin_name: &str = &args[1];
    let data_point_name: &str = &args[2];

    let weights = fs::read(model_bin_name)?;
    println!("Read graph weights, size in bytes: {}", weights.len());

    let graph = GraphBuilder::new(GraphEncoding::TensorflowLite, ExecutionTarget::CPU).build_from_bytes(&[&weights])?;
    let mut ctx = graph.init_execution_context()?;
    println!("Loaded graph into wasi-nn with ID: {}", graph);

    // Load a tensor that precisely matches the graph input tensor from a csv file
    let mut rdr = csv::Reader::from_reader(io::stdin());
    for result in rdr.records(){
        let record = result?;
        let tensor_data = record.iter().map(|x| x.parse::<u8>().unwrap()).collect::<Vec<u8>>();
        println!("Read input tensor, size in bytes: {}", tensor_data.len());
        //print tensor_data
        println!("{:?}", tensor_data);
        // Pass tensor data into the TFLite runtime
        ctx.set_input(&tensor_data)?;

        ctx.compute()?;

        let mut output_buffer = vec![0u8; 1];
        _ = ctx.get_output(&mut output_buffer)?;
    }
}