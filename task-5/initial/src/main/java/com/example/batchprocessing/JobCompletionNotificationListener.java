package com.example.batchprocessing;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobExecutionListener;
import org.springframework.jdbc.core.DataClassRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class JobCompletionNotificationListener implements JobExecutionListener {

	private static final Logger log = LoggerFactory.getLogger(JobCompletionNotificationListener.class);

	private final JdbcTemplate jdbcTemplate;
	private final Counter jobCompletedCounter;
	private final Counter jobFailedCounter;

	public JobCompletionNotificationListener(JdbcTemplate jdbcTemplate, MeterRegistry meterRegistry) {
		this.jdbcTemplate = jdbcTemplate;
		this.jobCompletedCounter = Counter.builder("batch.job.completed")
			.description("Number of completed jobs")
			.register(meterRegistry);
		this.jobFailedCounter = Counter.builder("batch.job.failed")
			.description("Number of failed jobs")
			.register(meterRegistry);
	}

	@Override
	public void afterJob(JobExecution jobExecution) {
		if (jobExecution.getStatus() == BatchStatus.COMPLETED) {
			log.info("!!! JOB FINISHED! Time to verify the results");
			jobCompletedCounter.increment();

			jdbcTemplate
					.query("SELECT productId, productSku, productName, productAmount, productData FROM products", new DataClassRowMapper<>(Product.class))
					.forEach(person -> log.info("Transformed <{}> in the database.", person));
		} else if (jobExecution.getStatus() == BatchStatus.FAILED) {
			log.error("!!! JOB FAILED!");
			jobFailedCounter.increment();
		}
	}
}
