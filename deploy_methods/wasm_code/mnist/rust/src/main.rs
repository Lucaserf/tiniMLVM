use std::time::{Instant, SystemTime};
use std::{env, error::Error, fs};
use wasi_nn::{ExecutionTarget, GraphBuilder, GraphEncoding, TensorType};

pub fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let model_bin_name: &str = &args[1];
    let data_point_name: &str = &args[2];

    let weights = fs::read(model_bin_name)?;
    // println!("Read graph weights, size in bytes: {}", weights.len());

    let graph = GraphBuilder::new(GraphEncoding::TensorflowLite, ExecutionTarget::CPU)
        .build_from_bytes(&[&weights])?;
    let mut ctx = graph.init_execution_context()?;
    // println!("Loaded graph into wasi-nn with ID: {}", graph);

    //read data points from csv file
    // println!("Reading data points from csv file: {:?}", data_point_name);

    println!("timestamp[ns],inference_time[ns]");
    let mut rdr = csv::Reader::from_path(data_point_name)?;
    for result in rdr.records() {
        let mut tensor_data = Vec::new();
        let record = result?;
        // println!("record: {:?}", record);
        for value in record.iter() {
            tensor_data.push(value.parse::<f32>()?);
        }
        //print data points
        // println!("tensor data: {:?}", tensor_data);
        // println!("Read input tensor, size in bytes: {}", tensor_data.len());

        //get probability output tensor
        let mut output_buffer = vec![0f32; 10];
        //get inference time
        let start = Instant::now();
        ctx.set_input(0, TensorType::F32, &[1, 28, 28, 1], &tensor_data)?;
        ctx.compute()?;
        _ = ctx.get_output(0, &mut output_buffer)?;
        let duration = start.elapsed();
        println!(
            "{},{}",
            SystemTime::now()
                .duration_since(SystemTime::UNIX_EPOCH)
                .unwrap()
                .as_nanos(),
            duration.as_nanos()
        );
        // println!("Inference time: {:?}", duration);

        // println!("Output tensor: {:?}", output_buffer);
    }

    Ok(())
}
