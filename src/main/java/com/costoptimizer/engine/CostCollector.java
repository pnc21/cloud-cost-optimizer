package com.costoptimizer.engine;

import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Component
public class CostCollector {
    
    @Autowired
    private MongoTemplate mongoTemplate;
    
    private Map<String, Double> costThresholds;

    public CostCollector() {
        this.costThresholds = new HashMap<>();
        // Default thresholds in USD
        costThresholds.put("AWS", 1000.0);
        costThresholds.put("Azure", 1000.0);
        costThresholds.put("GCP", 1000.0);
    }

    public void collectAwsCosts() {
        try {
            System.out.println("Collecting AWS costs...");
            // AWS cost collection logic here
            saveToDatabase("AWS", "Cost data collected");
        } catch (Exception e) {
            System.err.println("Error collecting AWS costs: " + e.getMessage());
        }
    }
    
    public void collectAzureCosts() {
        try {
            System.out.println("Collecting Azure costs...");
            saveToDatabase("Azure", "Cost data collected");
        } catch (Exception e) {
            System.err.println("Error collecting Azure costs: " + e.getMessage());
        }
    }
    
    public void collectGcpCosts() {
        try {
            System.out.println("Collecting GCP costs...");
            saveToDatabase("GCP", "Cost data collected");
        } catch (Exception e) {
            System.err.println("Error collecting GCP costs: " + e.getMessage());
        }
    }

    private void saveToDatabase(String provider, String data) {
        Map<String, Object> document = new HashMap<>();
        document.put("provider", provider);
        document.put("data", data);
        document.put("timestamp", System.currentTimeMillis());
        mongoTemplate.save(document, "cloud_costs");
    }
}