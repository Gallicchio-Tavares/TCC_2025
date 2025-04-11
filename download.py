#from pysus.ftp.databases.sinan import SINAN
from pysus.ftp.databases.sih import SIH
from pysus.ftp.databases.sim import SIM
import os
import pandas as pd
from tqdm import tqdm
import logging

def combine_parquet_files(folder_path, output_file):
    """
    Combine parquet files into a single parquet file

    Args:
    folder_path: str, folder containing the parquets
    output_file: str, output destination

    """
    try:
        if os.path.exists(output_file) and not os.path.isdir(output_file):
            logging.info(f"Combined parquet file already exists: {output_file}")    
            return

        dfs = []
        parquet_files = [f for f in os.listdir(folder_path) if f.endswith(".parquet")]

        for filename in tqdm(parquet_files, desc="Combining Parquet Files", unit="file"):
            file_path = os.path.join(folder_path, filename)
            dfs.append(pd.read_parquet(file_path))
            os.remove(os.path.join(folder_path, filename))
        os.rmdir(folder_path)

        combined_df = pd.concat(dfs, ignore_index=True)

        combined_df.to_parquet(output_file)
        logging.info(f"Combined parquet file created: {output_file}")
    except Exception as e:
        logging.error(f"Erro combining parquet files: {e}") 
           

# def download_sinan_file(disease, year, path):
#     """
#     Downloads a file from SUS FTP server to a local destination.

#     Args:
#     disease: SINAN disease
#     year: year in yyyy format
#     path: str, Destination path

#     """        
#     try:
#         os.makedirs(path, exist_ok=True)
#         sinan = SINAN().load()
#         files = sinan.get_files(disease, year)
#         if files:
#             sinan.download(files, local_dir=path)
#             logging.info(f"File {files[0]} downloaded at: {path}")
#             return files[0]
#     except Exception as e:
#         logging.error(f"Erro downloading file: {e}")    
#     return None

def download_sih_file():
    """
    Downloads a file from SUS FTP server to a local destination.

    Args:
    year: year in yyyy format
    uf: unidade federativa de sua escolha
    path: str, Destination path

    """        
    try:
        os.makedirs("data", exist_ok=True)
        sih = SIH().load()
        lista_grupos = ["RD", "RJ", "ER", "SP", "CH", "CM"]
        sih.describe("data/{}.DBC")
        files = sih.get_files(lista_grupos, "RJ", 2024)
        if files:
            sih.download(files, local_dir="data")
            logging.info(f"File {files[0]} downloaded at: data")
            return files[0]
    except Exception as e:
        logging.error(f"Erro downloading file: {e}")    
    return None

def download_sim_file():
    """
    Downloads a file from SUS FTP server to a local destination.

    Args:
    year: year in yyyy format
    uf: unidade federativa de sua escolha
    path: str, Destination path

    """        
    try:
        os.makedirs("data", exist_ok=True)
        sim = SIM().load()
        lista_grupos = ["CID10"]
        files = sim.get_files(lista_grupos, "RJ", 2024)
        if files:
            sim.download(files, local_dir="data")
            logging.info(f"File {files[0]} downloaded at: data")
            return files[0]
    except Exception as e:
        logging.error(f"Erro downloading file: {e}")    
    return None
            
def main():
    # parser = argparse.ArgumentParser(description="Download SINAN disease file from SUS")
    #parser.add_argument("disease", nargs="?", help="SINAN disease, default is DENG", default="DENG")
    
    # parser.add_argument("year", help="Date in yyyy format, default is current year", default=None)
    # parser.add_argument("UF", default="RJ")
    # parser.add_argument("path", help="Destination path, default is data/raw", default="data/raw")
    # parser.add_argument("--log", dest="log_level", choices=["INFO", "DEBUG", "ERROR"], default="DEBUG", help="Set the logging level")
    
    # args = parser.parse_args()

    # if args.year is None:
    #     args.year = datetime.date.today().year
            
    # logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s - %(levelname)s - %(message)s")    

    downloaded_file = download_sim_file()
    file_path = f"data/{downloaded_file.name}.parquet"
    if downloaded_file:
        combine_parquet_files(file_path, file_path)

if __name__ == "__main__":
    main()