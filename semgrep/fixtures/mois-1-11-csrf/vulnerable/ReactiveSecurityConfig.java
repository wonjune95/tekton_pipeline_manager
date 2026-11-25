package demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

// 탐지돼야 하는 경우: WebFlux 설정에서 CSRF 토큰 검사를 끔
@Configuration
public class ReactiveSecurityConfig {
    @Bean
    public SecurityWebFilterChain filterChain(ServerHttpSecurity http) {
        // ruleid: mois-1-11-csrf
        return http.csrf(ServerHttpSecurity.CsrfSpec::disable).build();
    }
}
