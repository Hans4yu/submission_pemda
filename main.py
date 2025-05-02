import logging
from datetime import datetime
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_postgresql, save_to_gsheet_api


def setup_logging():
    """Configure logging for the ETL pipeline"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('etl_pipeline.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def run_etl_pipeline():
    """Main ETL pipeline executor"""
    try:
        logging.info("[START] Starting ETL Pipeline")
        start_time = datetime.now()

        logging.info("[EXTRACT] Starting Extraction Phase")
        raw_data = extract_data()
        logging.info(f"[EXTRACT] Successfully extracted {len(raw_data)} items")

        logging.info("[TRANSFORM] Starting Transformation Phase")
        transformed_data = transform_data(raw_data)
        logging.info(f"[TRANSFORM] Transformed {len(transformed_data)} records")

        logging.info("[LOAD] Saving to CSV")
        if save_to_csv(transformed_data, "products.csv"):
            logging.info("[CSV] Data successfully saved to output.csv")
        else:
            logging.error("[CSV] Failed to save data to CSV")

        logging.info("[LOAD] Saving to PostgreSQL")
        postgres_url = "postgresql://etl_user:admin@localhost:5432/etl_db"  # Ganti sesuai koneksi kamu
        if save_to_postgresql(transformed_data, db_url=postgres_url, table_name="etl_data"):
            logging.info("[POSTGRESQL] Data successfully saved to PostgreSQL")
        else:
            logging.error("[POSTGRESQL] Failed to save data to PostgreSQL")


        logging.info("[LOAD] Saving to Google Sheets")
        if save_to_gsheet_api(transformed_data, spreadsheet_id="1kFWmD61oAWMN5w1bO7UFVej9XKi0bF0RYnKfeoqIi24", range_name="Sheet1!A1", json_key_path="google-sheets-api.json"):
            logging.info("[GSHEET] Data uploaded to Google Sheets successfully")
        else:
            logging.error("[GSHEET] Failed to upload to Google Sheets")


        duration = datetime.now() - start_time
        logging.info(f"[DONE] ETL Pipeline completed in {duration.total_seconds():.2f} seconds")

    except Exception as e:
        logging.error(f"[CRITICAL] Pipeline failure: {str(e)}", exc_info=True)

if __name__ == "__main__":
    setup_logging()
    run_etl_pipeline()