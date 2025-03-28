package com.dvFabricio.BMEH.infra.exception.resource;

import lombok.Getter;


import java.time.Instant;
import java.util.ArrayList;
import java.util.List;


@Getter
public class ValidationError extends StandardError {

    private final List<FieldMessage> errors = new ArrayList<>();

    public ValidationError(Instant timestamp, int status, String error, String message, String path) {
        super(timestamp, status, error, message, path);
    }

    public void addError(String fieldName, String message) {
        errors.add(new FieldMessage(fieldName, message));
    }
}
