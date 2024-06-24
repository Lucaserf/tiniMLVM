use std::{env, error::Error, fs};
use wasi_nn::{ExecutionTarget, GraphBuilder, GraphEncoding, TensorType};

pub fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let model_bin_name: &str = &args[1];
    let data_point_name: &str = &args[2];

    let weights = fs::read(model_bin_name)?;
    println!("Read graph weights, size in bytes: {}", weights.len());

    let graph = GraphBuilder::new(GraphEncoding::TensorflowLite, ExecutionTarget::CPU)
        .build_from_bytes(&[&weights])?;
    let mut ctx = graph.init_execution_context()?;
    println!("Loaded graph into wasi-nn with ID: {}", graph);

    //read data points from csv file
    println!("Reading data points from csv file: {:?}", data_point_name);
    let mut rdr = csv::Reader::from_path(data_point_name)?;
    let mut tensor_data = vec![];
    for result in rdr.records() {
        let record = result?;
        println!("record: {:?}", record);
        for value in record.iter() {
            tensor_data.push(value.parse::<f32>()?);
        }
    }
    //print data points
    println!("tensor data: {:?}", tensor_data);
    println!("Read input tensor, size in bytes: {}", tensor_data.len());
    ctx.set_input(0, TensorType::F32, &[1, 10], &tensor_data)?;

    ctx.compute()?;

    let mut output_buffer = vec![0f32; 1];
    _ = ctx.get_output(0, &mut output_buffer)?;

    println!("Output tensor: {:?}", output_buffer);

    Ok(())
}
